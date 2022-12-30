name: Update Filters
on:
  schedule:
    - cron:  '0 10 * * *'
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:

      - name: Checkout
        uses: actions/checkout@v2

      - name: Run update-filters.sh
        run: |
          chmod +x ruleset_converter update-filters.sh
          ./update-filters.sh

      - name: Generate date
        run: echo "DATE=$(date +%F-%H-%M)" >> $GITHUB_ENV

      - name: Commit filters
        uses: EndBug/add-and-commit@v9.1.1
        with:
          add: 'filters.dat'
          default_author: github_actions
          message: 'Update filters: ${{ env.DATE }}'
          push: true

