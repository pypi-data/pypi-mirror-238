class AddTranscriptTable < ActiveRecord::Migration[6.1]
  def change
    create_table :transcripts do |t|
      t.timestamps
      t.string :ensembl_id, null: false
      t.integer :tsl, null: false
      t.integer :length, null: false
      t.string :biotype, null: false
    end

    add_reference :transcripts, :gene, foreign_key: true, null: false, index: true

    add_index :transcripts, :ensembl_id
  end
end
