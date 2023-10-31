const AbstractHandler = require("./AbstractHandler")


class ArrayGetSizeHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 1

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Array Get Size parameters mismatch")
            }
            let array = command.payload[0]
            return array.length
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new ArrayGetSizeHandler()