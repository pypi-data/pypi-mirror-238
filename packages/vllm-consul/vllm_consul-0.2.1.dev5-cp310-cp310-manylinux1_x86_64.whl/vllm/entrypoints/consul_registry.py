import asyncio
import consul.aio
import os

class ConsulClient:
    def __init__(self) -> None:
        consul_addr = os.getenv('APP_CONSUL_ADDRESS')
        host, port = consul_addr.split(':')
        self.client = consul.aio.Consul(host=host, port=int(port))

    async def register(self, server_name: str, port: int):
        pod_ip = os.getenv('POD_IP')
        await self.client.agent.service.register(
            name=server_name,
            service_id="%s_%s" % (server_name, pod_ip),
            address=pod_ip,
            port=port,
            check=consul.Check.tcp(pod_ip, port, "5s", "10s", "20s"),
        )

if __name__ == "__main__":
    server_name = os.getenv("SERVER_NAME") or "llm-qwen-openai"
    asyncio.get_event_loop().run_until_complete(ConsulClient().register(server_name, 8000))
    print("Consul done")