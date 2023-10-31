require_relative 'abstract_command_handler'

class ArraySetItemHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 3
  end
  def process(command)
    begin
      if command.payload.length < @required_parameters_count
        raise ArgumentError.new "Array set item parameters mismatch"
      end
      array = command.payload[0]
      value = command.payload[1]
      index = command.payload[2,]
      array[index] = value
      return 0
    rescue Exception => e
      return e
    end
  end
end