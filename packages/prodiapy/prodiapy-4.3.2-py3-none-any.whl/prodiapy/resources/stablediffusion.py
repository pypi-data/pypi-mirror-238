
from prodiapy.resources.engine import Engine
from prodiapy.log_util import failed, success
import time
import asyncio


class StableDiffusion(Engine):
    def __init__(self, api_key, base_url=None):
        """
        Parameters:
            api_key: Your Personal API key, more on https://docs.prodia.com/reference/getting-started-guide
            base_url: Base url for requests
        """
        self.base = base_url or "https://api.prodia.com/v1"
        self.api_key = api_key

    def generate(self, **params):
        """
        Use this endpoint to start generating an image on Prodia.

        Parameters:
            params: keyword arguments containing generation data, more on https://docs.prodia.com/reference/generate
        Example:
            from prodiapy import StableDiffusion

            pipe = StableDiffusion("YOUR-API-KEY")

            job = pipe.generate(prompt="cat")
            ...
        """
        return super()._post(url=f"{self.base}/sd/generate", body=params, api_key=self.api_key)

    def transform(self, **params):
        """
        Use this endpoint to do an 'img2img' style generation.

        Parameters:
            params: keyword arguments containing generation data, more on https://docs.prodia.com/reference/transform
        Example:
            from prodiapy import StableDiffusion

            pipe = StableDiffusion("YOUR-API-KEY")

            job = pipe.transform(imageUrl="someurl.com/image.png", prompt="cat")
            ...
        """
        return super()._post(url=f"{self.base}/sd/transform", body=params, api_key=self.api_key)

    def inpainting(self, **params):
        """
        Use this endpoint to do an inpaint generation.

        Parameters:
            params: keyword arguments containing generation data, more on https://docs.prodia.com/reference/inpainting
        Example:
            from prodiapy import StableDiffusion

            pipe = StableDiffusion("YOUR-API-KEY")

            job = pipe.inpainting(imageUrl="someurl.com/image.png", maskUrl="someurl.com/mask.png", prompt="cat")
            ...
        """
        return super()._post(url=f"{self.base}/sd/inpainting", body=params, api_key=self.api_key)

    def controlnet(self, **params):
        """
        Use this endpoint to do a Controlnet generation.

        Parameters:
            params: keyword arguments containing generation data, more on https://docs.prodia.com/reference/controlnet
        Example:
            from prodiapy import StableDiffusion

            pipe = StableDiffusion("YOUR-API-KEY")

            job = pipe.controlnet(imageUrl="someurl.com/image.png", prompt="cat")
            ...
        """
        return super()._post(url=f"{self.base}/sd/controlnet", body=params, api_key=self.api_key)

    def get_job(self, job_id):
        """
        Get information about a generation job, including status.

        :param job_id: Job id
        :returns: JSON response
        """
        return super()._get(url=f"{self.base}/job/{job_id}", api_key=self.api_key)

    def models(self):
        """
        Get a list of current available SD 1.X models.
        """
        return super()._get(url=f"{self.base}/sd/models", api_key=self.api_key)

    def samplers(self):
        """
        Get a list of current available SD 1.X samplers.
        """
        return super()._get(url=f"{self.base}/sd/samplers", api_key=self.api_key)

    def loras(self):
        """
        Get a list of current available SD 1.X LoRa models.
        """
        return super()._get(url=f"{self.base}/sd/loras", api_key=self.api_key)

    def wait_for(self, job):
        job_result = job

        while job_result['status'] not in ['succeeded', 'failed']:
            time.sleep(0.25)
            job_result = self.get_job(job['job'])

        if job_result['status'] == 'failed':
            failed(f"Job {job_result['job']} failed")
            raise Exception("Job failed")

        success(f"Got result: {job_result}")
        return job_result


class AsyncStableDiffusion(Engine):
    def __init__(self, api_key, base_url=None):
        self.base = base_url or "https://api.prodia.com/v1"
        self.api_key = api_key

    async def generate(self, **params):
        return await super()._apost(url=f"{self.base}/sd/generate", body=params, api_key=self.api_key)

    async def transform(self, **params):
        return await super()._apost(url=f"{self.base}/sd/transform", body=params, api_key=self.api_key)

    async def inpainting(self, **params):
        return await super()._apost(url=f"{self.base}/sd/inpainting", body=params, api_key=self.api_key)

    async def controlnet(self, **params):
        return await super()._apost(url=f"{self.base}/sd/controlnet", body=params, api_key=self.api_key)

    async def get_job(self, job_id):
        return await super()._aget(url=f"{self.base}/job/{job_id}", api_key=self.api_key)

    async def models(self):
        return await super()._aget(url=f"{self.base}/sd/models", api_key=self.api_key)

    async def samplers(self):
        return await super()._aget(url=f"{self.base}/sd/samplers", api_key=self.api_key)

    async def loras(self):
        return await super()._aget(url=f"{self.base}/sd/loras", api_key=self.api_key)

    async def wait_for(self, job):
        job_result = job

        while job_result['status'] not in ['succeeded', 'failed']:
            await asyncio.sleep(0.25)
            job_result = await self.get_job(job['job'])

        if job_result['status'] == 'failed':
            failed(f"Job {job_result['job']} failed")
            raise Exception("Job failed")

        success(f"Got result: {job_result}")
        return job_result
