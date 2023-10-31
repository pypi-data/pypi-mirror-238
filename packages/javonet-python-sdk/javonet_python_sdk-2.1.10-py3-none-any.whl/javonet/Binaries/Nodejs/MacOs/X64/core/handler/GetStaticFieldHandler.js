const AbstractHandler = require("./AbstractHandler");

class GetStaticFieldHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 2

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Array Static Field parameters mismatch")
            }
            const {payload} = command
            let type = payload[0]
            let field = payload[1]

            let staticField = type[field]
            if (typeof(staticField) === 'undefined') {
                throw new Error("Static field does not exist")
            }
            else {
                return staticField
            }
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}


module.exports = new GetStaticFieldHandler()