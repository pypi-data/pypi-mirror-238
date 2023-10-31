const AbstractHandler = require("./AbstractHandler");

class CreateClassInstanceHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 1

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Create Class Instance parameters mismatch")
            }
            let clazz = command.payload[0]
            let constructorArguments = command.payload.slice(1)
            let instance = new clazz(...constructorArguments)
            if (typeof(instance) == 'undefined') {
                throw "Instance cannot be created"
            } else {
                return instance
            }
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new CreateClassInstanceHandler()