import asyncio

async def asyn_ping(ipAddr : str):

    cmd = 'ping -n 1 ' + ipAddr 
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()


    if stderr:
        return (stderr.decode())

    if ('TTL' in stdout.decode()):
        return ipAddr


async def main_ping(ipAddressThreeOctate):
    pingResult = await asyncio.gather(*[asyn_ping(ipAddressThreeOctate + ".{}".format(i)) for i in range(1, 255)])
    pingOK = [i for i in pingResult if i is not None]
    return (pingOK)


# result = asyncio.run(main_ping("192.168.0"))


#   usage:
#       from asyncioping import main_ping
#       result = asyncio.run(main_ping("192.168.0"))
