const AbstractHandler = require("./AbstractHandler")


class ArraySetItemHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 3

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Array Set Item parameters mismatch")
            }

            let array = command.payload[0]
            let value = command.payload[1]
            let indexes = command.payload.slice(2)
            array[indexes] = value
            return 0;
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new ArraySetItemHandler()