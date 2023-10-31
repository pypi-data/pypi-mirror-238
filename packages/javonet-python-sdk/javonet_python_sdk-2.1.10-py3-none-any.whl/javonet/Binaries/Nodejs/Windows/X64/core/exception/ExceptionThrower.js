const ExceptionType = require("../../utils/ExceptionType");


class ExceptionThrower {

    static throwException(commandException) {
        let javonetStackCommand = commandException.payload[1];
        let exceptionName = commandException.payload[2];
        let exceptionMessage =  commandException.payload[3];

        let stackTraceClasses = commandException.payload[4];
        let stackTraceMethods = commandException.payload[5];
        let stackTraceLines = commandException.payload[6];
        let stackTraceFiles = commandException.payload[7];

        let exceptionType = commandException.payload[0];

        let error
        switch (exceptionType) {
            case ExceptionType.EXCEPTION:
            case ExceptionType.IO_EXCEPTION:
            case ExceptionType.FILE_NOT_FOUND_EXCEPTION:
            case ExceptionType.RUNTIME_EXCEPTION:
            case ExceptionType.ARITHMETIC_EXCEPTION:
                error = new Error()
            case ExceptionType.ILLEGAL_ARGUMENT_EXCEPTION:
            case ExceptionType.NULL_POINTER_EXCEPTION:
                error = new TypeError()
            case ExceptionType.INDEX_OUT_OF_BOUNDS_EXCEPTION:
                error = new RangeError()
            default:
                error = new Error()
        }
        error.stack = this.serializeStack(stackTraceClasses, stackTraceMethods, stackTraceLines, stackTraceFiles)
        error.name = exceptionName
        error.message = exceptionMessage
        //error.path = javonetStackCommand
        return error
    }

    static serializeStack(stackTraceClasses, stackTraceMethods, stackTraceLines, stackTraceFiles) {
        let stackTraceClassesArray = stackTraceClasses.split('|')
        let stackTraceMethodsArray = stackTraceMethods.split('|')
        let stackTraceLinesArray = stackTraceLines.split('|')
        let stackTraceFilesArray = stackTraceFiles.split('|')

        let stackTrace = "";

        for (let i = 0; i < stackTraceClassesArray.length; i++) {
            if (stackTraceClassesArray[i] != "") {
                stackTrace += `    at ${stackTraceClassesArray[i]}`;
            }
            if (i < stackTraceMethodsArray.length && stackTraceMethodsArray[i] != "") {
                stackTrace += `.${stackTraceMethodsArray[i]}`
            }
            if (i < stackTraceFilesArray.length && stackTraceFilesArray[i] != "") {
                stackTrace += ` ${stackTraceFilesArray[i]}`
            }
            if (i < stackTraceLinesArray.length && stackTraceLinesArray[i] != "") {
                stackTrace += `:${stackTraceLinesArray[i]}`
            }
            stackTrace += "\n"

        }
        return stackTrace
    }
}
module.exports = ExceptionThrower