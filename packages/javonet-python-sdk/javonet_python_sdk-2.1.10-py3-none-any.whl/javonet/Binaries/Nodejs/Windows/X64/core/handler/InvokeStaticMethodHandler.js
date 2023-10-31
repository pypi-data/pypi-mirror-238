const AbstractHandler = require('./AbstractHandler')

class InvokeStaticMethodHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 2

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Invoke Static Method parameters mismatch")
            }
            const {payload} = command
            let type = payload[0]
            let methodName = payload[1]
            let args = payload.slice(2)
            let method = type[methodName]
            if (typeof(method) === 'undefined') {
                throw new Error("Static method does not exist")
            } else {
                return Reflect.apply(method, undefined, args)
            }
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new InvokeStaticMethodHandler()
