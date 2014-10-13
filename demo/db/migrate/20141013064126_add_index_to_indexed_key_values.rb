class AddIndexToIndexedKeyValues < ActiveRecord::Migration
  def change
    add_index :indexed_key_values, :key, unique: true
  end
end
