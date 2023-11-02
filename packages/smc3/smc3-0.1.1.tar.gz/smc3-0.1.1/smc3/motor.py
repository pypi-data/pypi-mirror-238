from typing import Tuple

from .protocol import Motor as MotorNumber, Parameter, read_command, parse_packet


class Motor:
    def __init__(self, number: MotorNumber):
        self.number = number

    async def get_position(self) -> Tuple[int, int]:
        cmd = read_command(self.number, Parameter.Position)
        _, _, target, feedback = await self.request_read(cmd)
        return target, feedback

    async def get_pwm_status(self) -> Tuple[int, int]:
        cmd = read_command(self.number, Parameter.PwmStatus)
        _, _, target, feedback = await self.request_read(cmd)
        return target, feedback

    async def get_Kp(self) -> int:
        return await self._read_coeff(Parameter.Kp)

    async def get_Ki(self) -> int:
        return await self._read_coeff(Parameter.Ki)

    async def get_Kd(self) -> int:
        return await self._read_coeff(Parameter.Kd)

    async def get_Ks(self) -> int:
        return await self._read_coeff(Parameter.Ks)

    async def _read_coeff(self, k: Parameter) -> int:
        cmd = read_command(self.number, k)
        _, _, kv = await self.request_read(cmd)
        return kv

    async def request_read(self, cmd: bytes) -> Any:
        # Send via serial
        # Receive response
        return parse_packet(cmd)  # Dummy

    async def _send_command(self, cmd: bytes) -> None:
        ...
