            if (arg1.constructor === Object) {
                i = 1;
                for (attrName in arg1) {
                    currentAttr = arg1[attrName]
                    if (attrName == "style") {
                        for (styleName in currentAttr) {
                            tag.style[styleName] = currentAttr[styleName];
                        }
                    } else {
                        tag[attrName] = currentAttr;
                    }
                }
            } else {
                i = 0;
            }