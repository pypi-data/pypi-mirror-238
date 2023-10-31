const AbstractHandler = require("./AbstractHandler");

class SetInstanceFieldHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 3

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Set Instance Field parameters mismatch")
            }
            const {payload} = command
            let instance = payload[0]
            let field = payload[1]
            let value = payload[2]
            if (typeof(instance[field]) === 'undefined') {
                throw new Error("Instance field does not exist")
            }
            instance[field] = value
            return 0
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new SetInstanceFieldHandler()