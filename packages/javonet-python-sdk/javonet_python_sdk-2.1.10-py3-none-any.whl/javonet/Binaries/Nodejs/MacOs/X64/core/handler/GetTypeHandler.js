const AbstractHandler = require("./AbstractHandler");

class GetTypeHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 1

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Get Type parameters mismatch")
            }
            const {payload} = command
            let typeName = payload[0]
            typeName = typeName.replace(".js", "")
            let type = global[typeName]
            if (type == undefined) {
                throw new Error(`Cannot load ${typeName}`)
            } else {
                return type
            }
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }

    }
}

module.exports = new GetTypeHandler()