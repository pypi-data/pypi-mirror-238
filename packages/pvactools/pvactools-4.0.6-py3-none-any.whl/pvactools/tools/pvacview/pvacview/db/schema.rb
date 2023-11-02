# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2023_08_01_182933) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "genes", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "name"
    t.string "ensembl_id", null: false
    t.index ["ensembl_id"], name: "index_genes_on_ensembl_id"
  end

  create_table "samples", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "name", null: false
    t.index ["name"], name: "index_samples_on_name"
  end

  create_table "transcripts", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "ensembl_id", null: false
    t.integer "tsl", null: false
    t.integer "length", null: false
    t.string "biotype", null: false
    t.bigint "gene_id", null: false
    t.index ["ensembl_id"], name: "index_transcripts_on_ensembl_id"
    t.index ["gene_id"], name: "index_transcripts_on_gene_id"
  end

  add_foreign_key "transcripts", "genes"
end
