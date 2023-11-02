class AddTranscriptTable < ActiveRecord::Migration[6.1]
  def change
    create_table :transcripts do |t|
      t.timestamps
      t.string :ensembl_id
      t.integer :tsl
      t.integer :length
      t.string :biotype
    end

    add_reference :transcripts, :gene, foreign_key: true

    add_index :transcripts, :ensembl_id
  end
end
