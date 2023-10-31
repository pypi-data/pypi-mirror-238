require_relative 'abstract_command_handler'

class ArrayGetSizeHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 1
  end
  def process(command)
    begin
      if command.payload.length < @required_parameters_count
        raise ArgumentError.new "Array get size parameters mismatch"
      end
      array = command.payload[0]
      return array.length()
    rescue Exception => e
      return e
    end
  end
end