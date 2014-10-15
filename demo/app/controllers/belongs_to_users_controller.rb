class BelongsToUsersController < ApplicationController
  skip_before_action :verify_authenticity_token
  def create
    begin
      @user = BelongsToUser.new(user_params)
      @user.belongs_to_department_id = user_params[:belongs_to_department_id]
      @user.save!
      puts @user.id
      render json: @user

    rescue ActiveRecord::RecordInvalid
      render plain: "ERROR"
    end
  end

  def destroy
    begin
      BelongsToUser.find(params[:id]).destroy
      render plain: "Deleted "+params[:id]
    rescue ActiveRecord::RecordNotFound
      render plain: params[:id]+" not found!"
    end
  end

private
  def user_params
    params.require(:belongs_to_user).permit(:id, :belongs_to_department_id) 
  end
end
