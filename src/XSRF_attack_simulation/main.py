import asyncio

import vulnerable
import evil

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server_task = loop.create_task(vulnerable.main())
    # client_task = loop.create_task(send_get("http://127.0.0.1:9999/login"))
    evil_task = loop.create_task(evil.main())
    aggregated_result = asyncio.gather(server_task, evil_task, return_exceptions=True)
    loop.run_until_complete(aggregated_result)
    loop.close()
    print(aggregated_result)



