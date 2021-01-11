# Translate ㊗️

If you love the terminal and you want an easy way to translate from it,
so **Translate CLI** can help you to translate and identify languages
using [BM Watson Language Translator](https://cloud.ibm.com/apidocs/language-translator?code=python#introduction), also you can add translations to your favorites
and see again any translation you have done before whenever you want.

## Setup 🧲

```bash
# Clone the repository
git clone https://github.com/ignite7/translate.git

# Go to the project
cd translate/cli

# Install translate-cli
pip install .

# Now you can use translete-cli command
translate-cli --help
```

## Usage example 📖

You need to create an account and login before to use it.

```bash
# Signup
translate-cli users signup -e <email> -u <username> -p <password prompt>

# Login
translate-cli users login -e <email> -p <password prompt>

# Translate
translate-cli translations translate -m "Hola mundo" -s es -t en

# Identify language
translate-cli translations identify -m "Thank you"

# See history or favorites
translate-cli histories list
translate-cli favorites list

# If you want to see all options
translate-cli --help
```

## To do ✔️

- Add Documentation translation service.
- Needs a UI.

## Thanks 👏🏻

> **_Made By:_** [Sergio van Berkel Acosta](https://www.sergiovanberkel.com/)
