from enum import Enum


class CommandType(Enum):
    Value = 0
    LoadLibrary = 1
    InvokeStaticMethod = 2
    GetStaticField = 3
    SetStaticField = 4
    CreateClassInstance = 5
    GetType = 6
    Reference = 7
    GetModule = 8
    InvokeInstanceMethod = 9
    Exception = 10
    HeartBeat = 11
    Cast = 12
    GetInstanceField = 13
    Optimize = 14
    GenerateLib = 15
    InvokeGlobalMethod = 16
    DestructReference = 17
    ArrayReference = 18
    ArrayGetItem = 19
    ArrayGetSize = 20
    ArrayGetRank = 21
    ArraySetItem = 22
    Array = 23
    RetrieveArray = 24
    SetInstanceField = 25
    InvokeGenericStaticMethod = 26
    InvokeGenericMethod = 27
    CreateGenericClassInstance = 28
    GetEnumItem = 29
    GetEnumName = 30
    GetEnumValue = 31
