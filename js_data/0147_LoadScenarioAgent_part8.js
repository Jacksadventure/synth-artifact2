      x = x.createSubContext({
        capabilityDAO: this.OrDAO.create({
          primary: this.ArrayDAO.create({
            of: 'foam.core.crunch.Capability',
            array: scenario.capabilities
          }),
          delegate: x.capabilityDAO
        }),
        prerequisiteCapabilityJunctionDAO: this.OrDAO.create({
          primary: this.ArrayDAO.create({
            of: 'foam.core.crunch.CapabilityCapabilityJunction',
            array: scenario.capabilityCapabilityJunctions
          }),
          delegate: x.prerequisiteCapabilityJunctionDAO
        })
      });