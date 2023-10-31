const AbstractHandler = require("./AbstractHandler");

class GetInstanceFieldHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 2

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Get Instance Field parameters mismatch")
            }
            const {payload} = command
            let instance = payload[0]
            let field = payload[1]
            let instanceField = instance[field]
            if (typeof(instanceField) === 'undefined') {
                throw new Error("Instance field does not exist")
            }
            else {
                return instanceField
            }
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new GetInstanceFieldHandler()