import fileinput

from utilities.utils_graphql import GraphQL
from utilities.utils import prepare_lines, write_entities

write_entities('./config/config.yml','demo')
write_entities('./config/config.yml','tag')
