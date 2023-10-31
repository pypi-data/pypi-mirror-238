const AbstractHandler = require("./AbstractHandler");

class InvokeGlobalMethodHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 1

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Invoke Global Method parameters mismatch")
            }
            const {payload} = command
            const splitted = payload[0].split(".")
            let methodToInvoke
            for (let i = 0; i < splitted.length; i++) {
                methodToInvoke = !methodToInvoke ? global[splitted[i]] : methodToInvoke[splitted[i]]
            }
            if(payload.length > 1) {
                const args = payload.slice(1)
                return methodToInvoke(args)
            } else {
                return methodToInvoke()
            }




        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }

}

module.exports = new InvokeGlobalMethodHandler()