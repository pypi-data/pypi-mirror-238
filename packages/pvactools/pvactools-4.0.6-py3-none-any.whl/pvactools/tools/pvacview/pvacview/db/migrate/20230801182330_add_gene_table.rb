class AddGeneTable < ActiveRecord::Migration[6.1]
  def change
    create_table :genes do |t|
      t.timestamps
      t.string :name
      t.string :ensembl_id, null: false
    end

    add_index :genes, :ensembl_id
  end
end
