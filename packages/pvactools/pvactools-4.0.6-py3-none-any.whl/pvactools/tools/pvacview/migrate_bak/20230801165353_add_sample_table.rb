class AddSampleTable < ActiveRecord::Migration[6.1]
  def change
    create_table :samples do |t|
      t.timestamps
      t.string :name
    end

    add_index :samples, :name
  end
end
