
from assertpy import assert_that

import netdot
import netdot.defaults


def test_generate_markdown_API_docs():
    # Arrange
    netdot.Repository.prepare_class()

    # Act
    docs = netdot.Repository.generate_markdown_docs()

    # ! SIDE EFFECT - Write updated documentation to file
    with open('docs/generated-api-docs.md', 'w') as f:
        f.write(docs)

    # Assert
    assert_that(docs[:1000].lower()).contains('# netdot python api generated documentation')
    assert_that(docs).contains('add_device')


def test_generate_ENV_VARs_help_docs():
    # Act
    docs = netdot.Repository.generate_markdown_docs_ENV_VARs()

    # ! SIDE EFFECT - Write updated documentation to file
    with open('docs/generated-env-var-docs.md', 'w') as f:
        f.write(docs)

    # Assert
    assert_that(docs).contains('NETDOT_CLI_TERSE')
