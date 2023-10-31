const AbstractHandler = require("./AbstractHandler")


class ArrayGetItemHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 2

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Array Get Item parameters mismatch")
            }
            let array = command.payload[0]
            let indexes = command.payload.slice(1)
            return array[indexes]
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new ArrayGetItemHandler()