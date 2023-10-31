const AbstractHandler = require("./AbstractHandler");

class InvokeInstanceMethodHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 2

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Invoke Instance Method parameters mismatch")
            }
            const {payload} = command
            let instance = payload[0]
            let methodName = payload[1]
            let args = payload.slice(2)
            let method = instance[methodName]
            if (typeof(method) === 'undefined') {
                throw new Error("Instance method does not exist")
            } else {
                return Reflect.apply(instance[methodName], undefined, args)
            }

        }
        catch (error){
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new InvokeInstanceMethodHandler()