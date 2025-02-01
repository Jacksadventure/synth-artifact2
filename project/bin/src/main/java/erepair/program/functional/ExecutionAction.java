package erepair.program.functional;

import erepair.program.subject.ExecutionInfo;

/**
 * @author Lukas Kirschner
 * @since 2019-06-04
 **/
@FunctionalInterface
public interface ExecutionAction {
    /**
     * @param action Execution Info from the subject
     */
    void run(ExecutionInfo action);
}
