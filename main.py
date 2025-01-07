from os import environ

from flask import Flask, jsonify, render_template, request
from requests import post

app = Flask(__name__)


def get_info(replit_id):
    out = (post(
        "https://replit.com/graphql",
        headers={
            "Referer": "https://replit.com",
            "X-Requested-With": "replit",
        },
        json={
            "variables": {
                "id": replit_id
            },
            "query":
            """
                    query Repl($id: String) {
                            repl(id: $id) {
                                    ... on Repl {
                                        id
                                        isProject
                                        isPrivate
                                        isStarred
                                        title
                                        slug
                                        imageUrl
                                        folderId 
                                        isRenamed
                                        commentCount
                                        likeCount
                                        currentUserDidLike
                                        templateCategory
                                        wasPosted
                                        wasPublished
                                        layoutState
                                        language
                                        owner: user {
                                            id
                                            username
                                        }
                                        origin {
                                            id
                                            title
                                            url
                                        }
                                        iconUrl
                                        templateLabel
                                        url
                                        multiplayerInvites {
                                            email
                                            replId
                                            type
                                        }
                                        rootOriginReplUrl
                                        timeCreated
                                        timeUpdated
                                        isOwner
                                        config {
                                            isServer
                                            gitRemoteUrl
                                            domain
                                            isVnc
                                            doClone
                                        }
                                        pinnedToProfile                          
                                        hostedUrl
                                        hostedUrlDotty: hostedUrl(dotty: true)
                                        hostedUrlDev: hostedUrl(dev: true)
                                        hostedUrlNoCustom: hostedUrl(noCustomDomain: true)
                                        currentUserPermissions {
                                            changeTitle
                                            changeDescription
                                            changeImageUrl
                                            changeIconUrl
                                            changeTemplateLabel
                                            changeLanguage
                                            changeConfig
                                            changePrivacy
                                            star
                                            move
                                            delete
                                            leaveMultiplayer
                                            editMultiplayers
                                            viewHistory
                                            containerAttach
                                            containerWrite
                                            changeAlwaysOn
                                            linkDomain
                                            changeCommentSettings
                                            inviteGuests
                                            publish
                                            fork
                                        }                   
                                        isProjectFork
                                        isModelSolution
                                        isModelSolutionFork
                                        workspaceCta                        
                                        publicForkCount
                                        runCount
                                        isAlwaysOn
                                        isBoosted
                                        tags {
                                            id
                                            isOfficial
                                        }
                                        lastPublishedAt
                                        multiplayers {
                                            username
                                        }
                                        nixedLanguage
                                        publishedAs             
                                        description(plainText: true)
                                        markdownDescription: description(plainText: false)
                                        templateInfo {
                                            label
                                            iconUrl
                                        }
                                        domains {
                                            domain
                                            state
                                        }
                                        replViewSettings {
                                            id
                                            defaultView
                                            replFile
                                            replImage
                                        }
                                    }
                            }
                    }
                """,
        },
    ).json())
    return ((out.get("data", out) or out).get("repl", out)) if out else None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get')
def repl_info():
    replit_id = request.args.get('replit_id') or environ.get('REPL_ID')

    if not replit_id:
        return jsonify({'error': 'replit_id is required'}), 400

    try:
        info = get_info(replit_id)
        if isinstance(info, dict) and request.args.get('title') is not None:
            info = info.get("title", "")
        return info if isinstance(info, str) else jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
