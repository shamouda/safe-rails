class IndexedKeyValuesController < ApplicationController
  skip_before_action :verify_authenticity_token
  def create
    begin
      @kvp = IndexedKeyValue.new(indexedkeyvalue_params)
      @kvp.save!
      puts @kvp.id
      render json: @kvp

    rescue ActiveRecord::RecordInvalid
      render plain: "ERROR"
    end
  end

  def update_key
    @kvp = IndexedKeyValue.find_by(key: indexedkeyvalue_params[:key])
    if @kvp
      @kvp.update!(indexedkeyvalue_params)
      render plain: "Success!"
    else
      render plain: "ERROR: nil"
    end
  end

  def get_key
    @kvp = IndexedKeyValue.find_by(key: indexedkeyvalue_params[:key])
    if @kvp
      render json: @kvp
    else
      render plain: "ERROR: nil"
    end
  end


  def index
    render json: IndexedKeyValue.all()
  end

  def destroy
    begin
      IndexedKeyValue.find(params[:id]).destroy
      render plain: "Deleted "+params[:id]
    rescue ActiveRecord::RecordNotFound
      render plain: params[:id]+" not found!"
    end
  end

  def destroy_key
    @nrec  = IndexedKeyValue.destroy_all(key: indexedkeyvalue_params[:key])
    render plain: "Destroyed "+@nrec.to_s
  end

  def delete_key
    @nrec  = IndexedKeyValue.delete_all(key: indexedkeyvalue_params[:key])
    render plain: "Destroyed "+@nrec.to_s
  end

  def destroy_all
    begin
      IndexedKeyValue.find_by_key(params[:key]) do |r| 
        r.destroy_all
      end
    end
  end


private
  def indexedkeyvalue_params
    params.require(:indexed_key_value).permit(:key, :value, :id)
  end
end
