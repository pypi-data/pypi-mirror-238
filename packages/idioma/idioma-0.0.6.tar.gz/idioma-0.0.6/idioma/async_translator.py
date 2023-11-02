# -*- coding: utf-8 -*-
"""
An Async Translation module.

You can translate text using this module, asynchronously.
"""
import httpx

from idioma import urls, utils
from idioma.async_gtoken import AsyncTokenAcquirer
from idioma.base_translator import BaseTranslator
from idioma.models import Detected
from idioma.retry_transport import RetryTransport


class AsyncTranslator(BaseTranslator):

    def _create_client(self) -> httpx.AsyncClient:
        # wrapped transport ensures that the client will retry on failure
        # of connections, not based on status codes
        # retry transport is used to retry on status codes
        retry_transport = RetryTransport(
            wrapped_transport=httpx.AsyncHTTPTransport(retries=10),
            retryable_methods={'GET', 'POST'},
            # Google would take too "sorry" page sometimes with 302
            retry_status_codes={302}
        )
        return httpx.AsyncClient(
            http2=self.http2,
            proxies=self.proxies,
            timeout=self.timeout,
            transport=retry_transport
        )

    def _get_token_acquirer(self):
        return AsyncTokenAcquirer(client=self.client,
                                  host=self.service_urls[0])

    async def prepare_translate_legacy_params(self, text, src, dest,
                                              override=None):
        token = ''  # dummy default value here as it is not used by api client
        if self.client_type == 'webapp':
            token = await self.token_acquirer.do(text)

        params = utils.build_params(client=self.client_type, query=text,
                                    src=src, dest=dest,
                                    token=token, override=override)

        url = urls.TRANSLATE.format(host=self._pick_service_url())
        return url, params

    async def _translate(self, text: str, dest: str, src: str):
        url = urls.TRANSLATE_RPC.format(host=self._pick_service_url())
        data = {
            'f.req': self._build_rpc_request(text, dest, src),
        }
        r = await self.client.post(url, params=self.POST_PARAMS, data=data)

        if r.status_code != 200 and self.raise_exception:
            raise Exception('Unexpected status code "{}" from {}'.format(
                r.status_code, self.service_urls))

        return r.text, r

    async def _translate_legacy(self, text, dest, src, override):

        url, params = await self.prepare_translate_legacy_params(text, src,
                                                                 dest,
                                                                 override)
        response = await self.client.get(url, params=params)
        return self.handle_legacy_translate_response(response, text)

    async def translate(self, text: str, dest='en', src=None):
        src, dest = self.validate_normalize_src_dest(src, dest)
        data, response = await self._translate(text, dest, src)
        return self.parse_response(src, dest, text, data, response)

    async def detect(self, text: str):
        translated = await self.translate(text, src='auto', dest='en')
        result = Detected(lang=translated.src,
                          confidence=translated.extra_data.get('confidence',
                                                               None),
                          response=translated._response)
        return result

    def detect_legacy(self, text, **kwargs):
        """Detect language of the input text

        :param text: The source text(s) whose language you want to identify.
                     Batch detection is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

        :rtype: Detected
        :rtype: :class:`list` (when a list is passed)

        Basic usage:
            >>> from idioma import AsyncTranslator
            >>> translator = AsyncTranslator()
            >>>  translator.detect('이 문장은 한글로 쓰여졌습니다.')
            <Detected lang=ko confidence=0.27041003>
            >>> translator.detect('この文章は日本語で書かれました。')
            <Detected lang=ja confidence=0.64889508>
            >>> translator.detect('This sentence is written in English.')
            <Detected lang=en confidence=0.22348526>
            >>> translator.detect('Tiu frazo estas skribita en Esperanto.')
            <Detected lang=eo confidence=0.10538048>

        Advanced usage:
            >>> langs = translator.detect(['한국어', '日本語', 'English', 'le français'])
            >>> for lang in langs:
            ...    print(lang.lang, lang.confidence)
            ko 1
            ja 0.92929292
            en 0.96954316
            fr 0.043500196
        """
        if isinstance(text, list):
            result = []
            for item in text:
                lang = self.detect(item)
                result.append(lang)
            return result

        data, response = self._translate_legacy(text, 'en', 'auto', kwargs)

        return self.extract_source_language_and_confidence(data, response)

    async def __aenter__(self):
        # Initialize the httpx.AsyncClient here
        self.client = self._create_client()

        if self.proxies is not None:
            self.client.proxies = self.proxies

        self.client.headers.update({
            'User-Agent': self.user_agent,
            'Referer': 'https://translate.google.com',
        })

        if self.timeout is not None:
            self.client.timeout = self.timeout

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # Close the httpx.AsyncClient when exiting the context
        await self.client.aclose()

    async def translate_legacy(self, text, dest='en', src='auto', **kwargs):
        """Translate text from source language to destination language

        :param text: The source text(s) to be translated. Batch translation is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

        :param dest: The language to translate the source text into.
                     The value should be one of the language codes listed in :const:`idioma.LANGUAGES`
                     or one of the language names listed in :const:`idioma.LANGCODES`.
        :param dest: :class:`str`; :class:`unicode`

        :param src: The language of the source text.
                    The value should be one of the language codes listed in :const:`idioma.LANGUAGES`
                    or one of the language names listed in :const:`idioma.LANGCODES`.
                    If a language is not specified,
                    the system will attempt to identify the source language automatically.
        :param src: :class:`str`; :class:`unicode`

        :rtype: Translated
        :rtype: :class:`list` (when a list is passed)

        Basic usage:
            >>> from idioma import Translator
            >>> translator = Translator()
            >>> translator.translate('안녕하세요.')
            <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
            >>> translator.translate('안녕하세요.', dest='ja')
            <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
            >>> translator.translate('veritas lux mea', src='la')
            <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

        Advanced usage:
            >>> translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
            >>> for translation in translations:
            ...    print(translation.origin, ' -> ', translation.text)
            The quick brown fox  ->  빠른 갈색 여우
            jumps over  ->  이상 점프
            the lazy dog  ->  게으른 개
        """
        src, dest = self.validate_normalize_src_dest(src, dest)

        if isinstance(text, list):
            result = []
            for item in text:
                translated = await self.translate_legacy(item, dest=dest,
                                                         src=src,
                                                         **kwargs)
                result.append(translated)
            return result

        data, response = self._translate_legacy(text, dest, src, kwargs)

        return self.parse_legacy_response(data, src, dest, text, response)
