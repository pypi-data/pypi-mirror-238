## -*- coding: utf-8; -*-

<%def name="tailbone_product_lookup_template()">
  <script type="text/x-template" id="tailbone-product-lookup-template">
    <div style="width: 100%;">

      <b-field grouped>

        <b-field :expanded="!product">
          <b-autocomplete ref="productAutocomplete"
                          v-if="!product"
                          v-model="autocompleteValue"
                          placeholder="Enter UPC or brand, description etc."
                          :data="autocompleteOptions"
                          field="value"
                          :custom-formatter="option => option.label"
                          @typing="getAutocompleteOptions"
                          @select="autocompleteSelected"
                          style="width: 100%;">
          </b-autocomplete>
          <b-button v-if="product"
                    @click="clearSelection(true)">
            {{ product.full_description }}
          </b-button>
        </b-field>

        <b-button type="is-primary"
                  v-if="!product"
                  @click="lookupInit()"
                  icon-pack="fas"
                  icon-left="search">
          Full Lookup
        </b-button>

        <b-button v-if="product"
                  type="is-primary"
                  tag="a" target="_blank"
                  :href="product.url"
                  :disabled="!product.url"
                  icon-pack="fas"
                  icon-left="external-link-alt">
          View Product
        </b-button>

      </b-field>

      <b-modal :active.sync="lookupShowDialog">
        <div class="card">
          <div class="card-content">

            <b-field grouped>

              <b-input v-model="searchTerm" 
                       ref="searchTermInput"
                       @keydown.native="searchTermInputKeydown">
              </b-input>

              <b-button class="control"
                        type="is-primary"
                        @click="performSearch()">
                Search
              </b-button>

              <b-checkbox v-model="searchProductKey"
                          native-value="true">
                ${request.rattail_config.product_key_title()}
              </b-checkbox>

              <b-checkbox v-model="searchVendorItemCode"
                          native-value="true">
                Vendor Code
              </b-checkbox>

              <b-checkbox v-model="searchAlternateCode"
                          native-value="true">
                Alt Code
              </b-checkbox>

              <b-checkbox v-model="searchProductBrand"
                          native-value="true">
                Brand
              </b-checkbox>

              <b-checkbox v-model="searchProductDescription"
                          native-value="true">
                Description
              </b-checkbox>

            </b-field>

            <b-table :data="searchResults"
                     narrowed
                     icon-pack="fas"
                     :loading="searchResultsLoading"
                     :selected.sync="searchResultSelected">

              <b-table-column label="${request.rattail_config.product_key_title()}"
                              field="product_key"
                              v-slot="props">
                {{ props.row.product_key }}
              </b-table-column>

              <b-table-column label="Brand"
                              field="brand_name"
                              v-slot="props">
                {{ props.row.brand_name }}
              </b-table-column>

              <b-table-column label="Description"
                              field="description"
                              v-slot="props">
                {{ props.row.description }}
                {{ props.row.size }}
              </b-table-column>

              <b-table-column label="Unit Price"
                              field="unit_price"
                              v-slot="props">
                {{ props.row.unit_price_display }}
              </b-table-column>

              <b-table-column label="Sale Price"
                              field="sale_price"
                              v-slot="props">
                <span class="has-background-warning">
                  {{ props.row.sale_price_display }}
                </span>
              </b-table-column>

              <b-table-column label="Sale Ends"
                              field="sale_ends"
                              v-slot="props">
                <span class="has-background-warning">
                  {{ props.row.sale_ends_display }}
                </span>
              </b-table-column>

              <b-table-column label="Department"
                              field="department_name"
                              v-slot="props">
                {{ props.row.department_name }}
              </b-table-column>

              <b-table-column label="Vendor"
                              field="vendor_name"
                              v-slot="props">
                {{ props.row.vendor_name }}
              </b-table-column>

              <b-table-column label="Actions"
                              v-slot="props">
                <a :href="props.row.url"
                   target="_blank"
                   class="grid-action">
                  <i class="fas fa-external-link-alt"></i>
                  View
                </a>
              </b-table-column>

              <template slot="empty">
                <div class="content has-text-grey has-text-centered">
                  <p>
                    <b-icon
                      pack="fas"
                      icon="fas fa-sad-tear"
                      size="is-large">
                    </b-icon>
                  </p>
                  <p>Nothing here.</p>
                </div>
              </template>
            </b-table>

            <br />
            <div class="level">
              <div class="level-left">
                <div class="level-item buttons">
                  <b-button @click="cancelDialog()">
                    Cancel
                  </b-button>
                  <b-button type="is-primary"
                            @click="selectResult()"
                            :disabled="!searchResultSelected">
                    Choose Selected
                  </b-button>
                </div>
              </div>
              <div class="level-right">
                <div class="level-item">
                  <span v-if="searchResultsElided"
                        class="has-text-danger">
                    {{ searchResultsElided }} results are not shown
                  </span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </b-modal>

    </div>
  </script>
</%def>

<%def name="tailbone_product_lookup_component()">
  <script type="text/javascript">

    const TailboneProductLookup = {
        template: '#tailbone-product-lookup-template',
        props: {
            product: {
                type: Object,
            },
            autocompleteUrl: {
                type: String,
                default: '${url('products.autocomplete')}',
            },
        },
        data() {
            return {
                autocompleteValue: '',
                autocompleteOptions: [],

                lookupShowDialog: false,

                searchTerm: null,
                searchTermLastUsed: null,

                searchProductKey: true,
                searchVendorItemCode: true,
                searchProductBrand: true,
                searchProductDescription: true,
                searchAlternateCode: true,

                searchResults: [],
                searchResultsLoading: false,
                searchResultsElided: 0,
                searchResultSelected: null,
            }
        },
        methods: {

            focus() {
                if (!this.product) {
                    this.$refs.productAutocomplete.focus()
                }
            },

            clearSelection(focus) {

                // clear data
                this.autocompleteValue = ''
                this.$emit('selected', null)

                // maybe set focus to our (autocomplete) component
                if (focus) {
                    this.$nextTick(() => {
                        this.focus()
                    })
                }
            },

            getAutocompleteOptions: debounce(function (entry) {

                // since the `@typing` event from buefy component does not
                // "self-regulate" in any way, we a) use `debounce` above,
                // but also b) skip the search unless we have at least 3
                // characters of input from user
                if (entry.length < 3) {
                    this.data = []
                    return
                }

                // and perform the search
                this.$http.get(this.autocompleteUrl + '?term=' + encodeURIComponent(entry))
                    .then(({ data }) => {
                        this.autocompleteOptions = data
                    }).catch((error) => {
                        this.autocompleteOptions = []
                        throw error
                    })
            }),

            autocompleteSelected(option) {
                this.$emit('selected', {
                    uuid: option.value,
                    full_description: option.label,
                    url: option.url,
                    image_url: option.image_url,
                })
            },

            lookupInit() {
                this.searchResultSelected = null
                this.lookupShowDialog = true

                this.$nextTick(() => {

                    this.searchTerm = this.autocompleteValue
                    if (this.searchTerm != this.searchTermLastUsed) {
                        this.searchTermLastUsed = null
                        this.performSearch()
                    }

                    this.$refs.searchTermInput.focus()
                })
            },

            searchTermInputKeydown(event) {
                if (event.which == 13) {
                    this.performSearch()
                }
            },

            performSearch() {
                if (this.searchResultsLoading) {
                    return
                }

                if (!this.searchTerm || !this.searchTerm.length) {
                    this.$refs.searchTermInput.focus()
                    return
                }

                this.searchResultsLoading = true
                this.searchResultSelected = null

                let url = '${url('products.search')}'
                let params = {
                    term: this.searchTerm,
                    search_product_key: this.searchProductKey,
                    search_vendor_code: this.searchVendorItemCode,
                    search_brand_name: this.searchProductBrand,
                    search_description: this.searchProductDescription,
                    search_alt_code: this.searchAlternateCode,
                }

                this.$http.get(url, {params: params}).then((response) => {
                    this.searchTermLastUsed = params.term
                    this.searchResults = response.data.results
                    this.searchResultsElided = response.data.elided
                    this.searchResultsLoading = false
                })
            },

            selectResult() {
                this.lookupShowDialog = false
                this.$emit('selected', this.searchResultSelected)
            },

            cancelDialog() {
                this.searchResultSelected = null
                this.lookupShowDialog = false
            },
        },
    }

    Vue.component('tailbone-product-lookup', TailboneProductLookup)

  </script>
</%def>
