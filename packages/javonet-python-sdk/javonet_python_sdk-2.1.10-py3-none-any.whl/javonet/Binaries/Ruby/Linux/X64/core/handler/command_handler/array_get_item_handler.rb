require_relative 'abstract_command_handler'

class ArrayGetItemHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 2
  end

  def process(command)
    begin
      if command.payload.length < @required_parameters_count
        raise ArgumentError.new "Array get item parameters mismatch"
      end
      array = command.payload[0]
      index = command.payload[1,]
      return array[index]
    rescue Exception => e
      return e
    end
  end
end