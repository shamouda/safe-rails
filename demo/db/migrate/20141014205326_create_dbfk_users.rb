class CreateDbfkUsers < ActiveRecord::Migration
  def change
    create_table :dbfk_users do |t|
      t.belongs_to :dbfk_department, index: true

      t.timestamps
    end
    add_foreign_key(:dbfk_users, :dbfk_departments)
  end
end
