package erepair.program.userinterface.actions.arguments;

import erepair.program.userinterface.actions.Argument;
import erepair.program.userinterface.actions.CliArgument;

/**
 * @author Lukas Kirschner
 * @since 2020-10-30
 **/
@CliArgument
public class TimeoutArg extends Argument {
    public TimeoutArg() {
        super('T', "timeouts", "Specify the timeouts per file in ms..");
    }
}
