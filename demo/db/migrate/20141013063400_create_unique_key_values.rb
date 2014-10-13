class CreateUniqueKeyValues < ActiveRecord::Migration
  def change
    create_table :unique_key_values do |t|
      t.string :key
      t.string :value

      t.timestamps
    end
  end
end
