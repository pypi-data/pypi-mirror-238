from javonet.core.exception.ExceptionThrower import ExceptionThrower
from javonet.core.interpreter.Interpreter import Interpreter
from javonet.utils.Command import Command
from javonet.utils.CommandType import CommandType

from javonet.utils.RuntimeName import RuntimeName
from javonet.utils.ConnectionType import ConnectionType
from javonet.sdk.internal.InvocationContext import InvocationContext
from javonet.sdk.internal.abstract.AbstractTypeContext import AbstractTypeContext


class RuntimeContext(AbstractTypeContext):

    __memory_runtime_contexts = dict()
    __network_runtime_contexts = dict()


    @staticmethod
    def get_instance(runtime_name: RuntimeName, connection_type: ConnectionType, tcp_address: str):
        if connection_type == ConnectionType.Tcp and tcp_address is not None:
            if tcp_address in RuntimeContext.__network_runtime_contexts:
                runtime_ctx = RuntimeContext.__network_runtime_contexts.get(tcp_address)
                runtime_ctx.current_command = None
                return runtime_ctx
            else:
                runtime_ctx = RuntimeContext(runtime_name, connection_type, tcp_address)
                RuntimeContext.__network_runtime_contexts[tcp_address] = runtime_ctx
                return runtime_ctx
        else:
            if runtime_name in RuntimeContext.__memory_runtime_contexts:
                runtime_ctx = RuntimeContext.__memory_runtime_contexts.get(runtime_name)
                runtime_ctx.current_command = None
                return runtime_ctx
            else:
                runtime_ctx = RuntimeContext(runtime_name, connection_type, None)
                RuntimeContext.__memory_runtime_contexts[runtime_name] = runtime_ctx
                return runtime_ctx

    def __init__(self, runtime_name: RuntimeName, connection_type: ConnectionType, tcp_address: str):
        self.__isExecuted = False
        self.__runtime_name = runtime_name
        self.__connection_type = connection_type
        self.__tcp_ip_address = tcp_address
        self.__python_interpreter = Interpreter()
        self.__current_command = None
        self.__response_command = None

    def execute(self, command: Command):
        self.__response_command = self.__python_interpreter.execute(command, self.__connection_type, self.__tcp_ip_address)
        self.__isExecuted = True
        if self.__response_command.command_type == CommandType.Exception:
            raise ExceptionThrower.throw_exception(self.__response_command)

    def load_library(self, *args):
        local_command = Command(self.__runtime_name, CommandType.LoadLibrary, [*args])
        self.execute(self.__build_command(local_command))
        return self

    def cast(self, *args):
        local_command = Command(self.__runtime_name, CommandType.Cast, [*args])
        return InvocationContext(self.__runtime_name, self.__connection_type, self.__tcp_ip_address,
                                 self.__build_command(local_command))

    def get_type(self, *args):
        local_command = Command(self.__runtime_name, CommandType.GetType, [*args])
        return InvocationContext(self.__runtime_name, self.__connection_type, self.__tcp_ip_address,
                                 self.__build_command(local_command))

    def get_enum_item(self, *args):
        local_command = Command(self.__runtime_name, CommandType.GetEnumItem, [*args])
        return InvocationContext(self.__runtime_name, self.__connection_type, self.__tcp_ip_address,
                                 self.__build_command(local_command))

    def __build_command(self, command):
        for i in range(len(command.payload)):
            command.payload[i] = self.__encapsulate_payload_item(command.payload[i])

        return command.prepend_arg_to_payload(self.__current_command)

    # encapsulate payload item into command
    def __encapsulate_payload_item(self, payload_item):
        if isinstance(payload_item, Command):
            for i in range(len(payload_item.payload)):
                payload_item.payload[i] = self.__encapsulate_payload_item(payload_item.payload[i])
            return payload_item

        elif isinstance(payload_item, InvocationContext):
            return payload_item.get_current_command()
        
        elif isinstance(payload_item, list):
            for i in range(len(payload_item)):
                payload_item[i] = self.__encapsulate_payload_item(payload_item[i])
            return Command(self.__runtime_name, CommandType.Array, payload_item)

        else:
            return Command(self.__runtime_name, CommandType.Value, [payload_item])
