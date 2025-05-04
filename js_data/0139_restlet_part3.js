                if (jsonResultId) {
                    task.create({
                        taskType: task.TaskType.MAP_REDUCE,
                        scriptId: "customscript_id_maprd",
                        deploymentId: "customdeploy_id_maprd",
                        params: {
                            custscript_lmry_ste_jsonresult_id: jsonResultId,
                            custscript_lmry_ste_transaction_id: transactionId
                        }
                    }).submit();
                }