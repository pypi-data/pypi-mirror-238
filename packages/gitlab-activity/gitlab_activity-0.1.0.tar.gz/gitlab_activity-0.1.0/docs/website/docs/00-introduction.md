---
id: intro
title: Introduction
slug: /
---

<!-- ../../../README.md -->

# GitLab Changelog Generator

[![ci](https://gitlab.com/mahendrapaipuri/gitlab-activity/badges/main/pipeline.svg)](https://gitlab.com/mahendrapaipuri/gitlab-activity/-/commits/main) [![codecov](https://codecov.io/gl/mahendrapaipuri/gitlab-activity/graph/badge.svg?token=O60VKC38YQ)](https://codecov.io/gl/mahendrapaipuri/gitlab-activity)

## What is it about?

Generate simple markdown changelogs for GitLab repositories. GitLab provides an
[API endpoint](https://docs.gitlab.com/ee/user/project/changelogs.html) to generate
Changelogs. However, this endpoint assumes that repository is using
[Git trailers](https://docs.gitlab.com/ee/user/project/changelogs.html) in the commit
message. If no Git trailers are found in the commit messages, the API endpoint returns nothing.

This is a huge problem for a lot of projects (including us) that do not use Git trailers.
Although it is a good practice to use Git trailers we tend to forget them and it
increases development time. Moreover we are more concerned to have MRs listed in the
changelogs and we can tag MRs with labels that identify the type of MR. We can
generate a changelog using these labels and group MRs according to the labels.

This is what this little package does to generate changelogs. In a nutshell, it does
two things:

1. Given a GitLab (upstream or self hosted) repository, an initial git reference or date,
   use the [GitLab GraphQL API](https://docs.gitlab.com/ee/api/graphql/reference/index.html)
   to return a DataFrame of all issue and MR activity for this time period.
2. A CLI to render this activity as markdown, suitable for generating changelogs.

## Prior art

- [gitlab-changelog-generator](https://github.com/stuartmccoll/gitlab-changelog-generator)
  is a command line utility distributed as Python package to generate changelogs.
  However, it is mostly outdated and I could not make it work as of 2023.
- [gitlab-changelog-generator](https://github.com/skywinder/gitlab-changelog-generator)
  is another tool to generate changelogs based on Ruby. However there has been no
  development since last few years.

## Features

- Users can configure the labels and their descriptions that they use in their projects
- `gitlab-activity` configuration supports `pyproject.toml` for Python projects,
  `package.json` for Node projects. For other projects, configuration can be included
  in a file `.gitlab-activity.toml` in the root of the repository.
- It can be integrated into CI release jobs to update the changelogs from last stable
  tag to current before making the release.

:::important

This tool is heavily inspired from
[github-activity](https://github.com/executablebooks/github-activity) developed by the
folks at [Jupyter project](https://jupyter.org/). All the credit should go to them
and we thank them for this super useful tool.

:::

## Installation

The easiest way to install this package is via `pip`:

```
pip install gitlab-activity
```

## Usage

The easiest way to use `gitlab-activity` to generate activity markdown is to use
the command-line interface. It takes the following form:

```
gitlab-activity -t [<group>/<repo>]
```

This will output a markdown with MRs activity since last tag.

## Configuration

All the CLI options can be configured _via_ configuration file. An example
[config](https://gitlab.com/mahendrapaipuri/gitlab-activity/-/blob/main/example-configs/.gitlab-activity.toml)
file can be used as a reference.

As stated above the configuration can be integrated into `pyproject.toml` in
`[tool.gitlab-activity]` section or `package.json` in `gitlab-activity` key.

## To run the tests

The easiest way to run the test suite is using `pytest`.

```
pytest
```
