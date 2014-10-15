class DbfkUsersController < ApplicationController
  skip_before_action :verify_authenticity_token
  def create
    begin
      @user = DbfkUser.new(user_params)
      @user.dbfk_department_id = user_params[:dbfk_department_id]
      @user.save!
      puts @user.id
      render json: @user

    rescue ActiveRecord::RecordInvalid
      render plain: "ERROR"
    end
  end

  def destroy
    begin
      DbfkUser.find(params[:id]).destroy
      render plain: "Deleted "+params[:id]
    rescue ActiveRecord::RecordNotFound
      render plain: params[:id]+" not found!"
    end
  end

private
  def user_params
    params.require(:dbfk_user).permit(:id, :dbfk_department_id) 
  end
end
