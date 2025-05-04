import { BaseObjectMapperConfiguration } from "../../../../shared/Infrastructure/Mapper/BaseObjectMapperConfiguration.js";
import { CollectionContainer } from "../Common/Containers/CollectionContainer.js";
import { GetNearEarthAsteroidsDto } from "./GetNearEarthAsteroidsDto.js";

class GetNearEarthAsteroidsMapperConfiguration extends BaseObjectMapperConfiguration {
    RegisterMapperConfiguration(mapper) {
        mapper.AddConfiguration(CollectionContainer, GetNearEarthAsteroidsDto, this.MapCollectionContainerToDto.bind(this));
    }

    MapCollectionContainerToDto(collectionContainer, dto) {
        dto.asteroids = collectionContainer.data;
    }
}

export { GetNearEarthAsteroidsMapperConfiguration };
