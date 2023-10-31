require_relative 'abstract_command_handler'

class SetInstanceFieldHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 3
  end

  def process(command)
    return set_instance_field(command)
  end

  def set_instance_field(command)
    begin
      if command.payload.length < @required_parameters_count
        raise ArgumentError.new "Set Instance Field parameters mismatch"
      end
      merged_value = '@' + command.payload[1]
      if command.payload[0].instance_variable_defined?(merged_value)
        command.payload[0].instance_variable_set(merged_value, command.payload[2])
      else
        raise "Instance field not defined"
      end
    rescue Exception => e
      return e
    end
  end
end
