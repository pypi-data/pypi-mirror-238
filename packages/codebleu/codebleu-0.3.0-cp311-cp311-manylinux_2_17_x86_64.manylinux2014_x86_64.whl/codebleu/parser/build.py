# Copyright (c) Microsoft Corporation.
# Copyright (c) 2023 Konstantin Chernyshev.
# Licensed under the MIT license.

from tree_sitter import Language

Language.build_library(
    "my-languages.so",
    [
        "tree-sitter/go",
        "tree-sitter/javascript",
        "tree-sitter/python",
        "tree-sitter/php",
        "tree-sitter/java",
        "tree-sitter/ruby",
        "tree-sitter/c-sharp",
        "tree-sitter/c",
        "tree-sitter/cpp",
    ],
)
