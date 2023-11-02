
from assertpy import assert_that

import netdot


def test_generate_markdown_docs():
    # Arrange
    netdot.Repository.prepare_class()

    # Act
    docs = netdot.Repository.generate_markdown_docs()

    # SIDE EFFECT - Write to file
    with open('docs/generated.md', 'w') as f:
        f.write(docs)

    # Assert
    assert_that(docs[:1000].lower()).contains('# netdot python api generated documentation')
    assert_that(docs).contains('add_device')
