class CreateSimpleKeyValues < ActiveRecord::Migration
  def change
    create_table :simple_key_values do |t|
      t.string :key
      t.string :value

      t.timestamps
    end
  end
end
