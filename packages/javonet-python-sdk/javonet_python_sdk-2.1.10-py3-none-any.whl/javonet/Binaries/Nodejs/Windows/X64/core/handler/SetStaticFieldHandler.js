const AbstractHandler = require('./AbstractHandler')

class SetStaticFieldHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 3

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Set static field parameters mismatch")
            }
            const {payload} = command
            let [obj, field, value] = payload
            if (typeof(obj[field]) === 'undefined') {
                throw new Error("Static field does not exist")
            }
            obj[field] = value
            return 0
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }

    }
}

module.exports = new SetStaticFieldHandler()