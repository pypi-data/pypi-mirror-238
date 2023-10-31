# `inferless`

Inferless - Deploy Machine Learning Models in Minutes.

See the website at https://inferless.com/ for documentation and more information
about running code on Inferless.

**Usage**:

```console
$ inferless [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`
* `--help`: Show this message and exit.

**Commands**:

* `deploy`: Initialize a new Inferless model
* `init`: Initialize a new Inferless model
* `login`: Login to Inferless
* `model`: Manage Inferless models
* `token`: Manage Inferless tokens
* `workspace`: Manage Inferless workspaces

## `inferless deploy`

Initialize a new Inferless model

**Usage**:

```console
$ inferless deploy [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless init`

Initialize a new Inferless model

**Usage**:

```console
$ inferless init [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless login`

Login to Inferless

**Usage**:

```console
$ inferless login [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless model`

Manage Inferless models

**Usage**:

```console
$ inferless model [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `activate`: activate a model.
* `deactivate`: deactivate a model.
* `delete`: delete a model.
* `list`: List all models.
* `rebuild`: rebuild a model.

### `inferless model activate`

activate a model.

**Usage**:

```console
$ inferless model activate [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model deactivate`

deactivate a model.

**Usage**:

```console
$ inferless model deactivate [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model delete`

delete a model.

**Usage**:

```console
$ inferless model delete [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model list`

List all models.

**Usage**:

```console
$ inferless model list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `inferless model rebuild`

rebuild a model.

**Usage**:

```console
$ inferless model rebuild [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

## `inferless token`

Manage Inferless tokens

**Usage**:

```console
$ inferless token [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `set`: Set account credentials for connecting to...

### `inferless token set`

Set account credentials for connecting to Inferless. If not provided with the command, you will be prompted to enter your credentials.

**Usage**:

```console
$ inferless token set [OPTIONS]
```

**Options**:

* `--token-key TEXT`: Account CLI key  [required]
* `--token-secret TEXT`: Account CLI secret  [required]
* `--help`: Show this message and exit.

## `inferless workspace`

Manage Inferless workspaces

**Usage**:

```console
$ inferless workspace [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `use`

### `inferless workspace use`

**Usage**:

```console
$ inferless workspace use [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
