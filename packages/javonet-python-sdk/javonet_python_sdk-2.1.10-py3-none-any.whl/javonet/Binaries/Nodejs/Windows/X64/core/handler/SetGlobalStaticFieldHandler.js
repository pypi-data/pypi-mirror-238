const AbstractHandler = require("./AbstractHandler")

class SetGlobalStaticFieldHandler extends AbstractHandler {
    constructor() {
        super()
    }

    requiredParametersCount = 2

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error("Set gloabal static field parameters mismatch")
            }
            const {payload} = command
            const splitted = payload[0].split(".")
            const value = payload[1]
            let fieldToSet

            for (let i = 0; i < splitted.length; i++) {
                fieldToSet = !fieldToSet ? global[splitted[i]] : fieldToSet[splitted[i]]
            }
            fieldToSet = value
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new SetGlobalStaticFieldHandler()