import asyncio
import io
import httpx
import soundfile as sf


def create_async_http_client(base_url: str):
    return httpx.AsyncClient(
        base_url=base_url,
    )

async def text_to_voice(text: str, voice_id: str = "male_1") -> bytes:

    async with create_async_http_client('https://vimbox-tts.osmi.com') as http_client:

        response = await http_client.get(
            '/api/v1/tts',
            params={
                'lang': 'en',
                'voice': voice_id,
                'text': text,
                'forceTtsEngine': 'polly',
            },
            timeout=30,
        )

        return response.read()

async def main():
    base_text: str = 'This is the best experience I have ever had'

    audio_bytes: bytes = await text_to_voice(base_text)

    audiodata, samplerate = sf.read(io.BytesIO(audio_bytes))

    sf.write("output.wav", audiodata, samplerate)


asyncio.run(main())

