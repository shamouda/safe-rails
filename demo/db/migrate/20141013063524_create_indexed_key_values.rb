class CreateIndexedKeyValues < ActiveRecord::Migration
  def change
    create_table :indexed_key_values do |t|
      t.string :key
      t.string :value

      t.timestamps
    end
  end
end
